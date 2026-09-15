const express = require("express");
const cors = require("cors");
const helmet = require("helmet");
const rateLimit = require("express-rate-limit");
const jwt = require("jsonwebtoken");
const Redis = require("ioredis");
const { Pool } = require("pg");

const app = express();
const PORT = process.env.PORT || 3001;
const JWT_SECRET = process.env.JWT_SECRET || "local-development-jwt-secret-change-me";
const notificationsUrl = process.env.NOTIFICATIONS_URL || "http://notifications-service:3002";
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const redis = new Redis(process.env.REDIS_URL || "redis://localhost:6379", { lazyConnect: true, maxRetriesPerRequest: 1 });
redis.connect().catch(() => {});
redis.on("error", () => {});

app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(rateLimit({ windowMs: 15 * 60 * 1000, limit: 100 }));

function requireAuth(req, res, next) {
    const token = req.headers.authorization?.replace("Bearer ", "");
    if (!token) {
        return res.status(401).json({ error: "Bearer token required" });
    }

    try {
        req.user = jwt.verify(token, JWT_SECRET);
        return next();
    } catch {
        return res.status(401).json({ error: "Invalid or expired token" });
    }
}

app.get("/health", (req, res) => {
    res.json({
        service: "orders-service",
        status: "healthy"
    });
});

app.get("/orders", requireAuth, async (req, res) => {
    try {
        const cacheKey = `orders:user:${req.user.sub}`;
        const cached = await redis.get(cacheKey).catch(() => null);
        if (cached) {
            return res.json({ service: "orders-service", orders: JSON.parse(cached), source: "redis" });
        }

        const result = await pool.query("SELECT id, user_id, product, quantity, status, created_at FROM orders WHERE user_id = $1 ORDER BY created_at DESC", [req.user.sub]);
        await redis.set(cacheKey, JSON.stringify(result.rows), "EX", 30).catch(() => {});
        return res.json({ service: "orders-service", orders: result.rows, source: "postgres" });
    } catch (error) {
        console.error(error);
        return res.status(500).json({ error: "Unable to retrieve orders" });
    }
});

app.get("/orders/:id", requireAuth, async (req, res) => {
    try {
        const result = await pool.query("SELECT id, user_id, product, quantity, status, created_at FROM orders WHERE id = $1 AND user_id = $2", [req.params.id, req.user.sub]);
        if (!result.rows[0]) return res.status(404).json({ error: "Order not found" });
        return res.json(result.rows[0]);
    } catch (error) {
        return res.status(500).json({ error: "Unable to retrieve order" });
    }
});

app.post("/orders", requireAuth, async (req, res) => {
    const { product, quantity } = req.body;
    if (typeof product !== "string" || product.trim().length < 2 || !Number.isInteger(quantity) || quantity < 1) {
        return res.status(400).json({ error: "Product and a positive integer quantity are required" });
    }

    const client = await pool.connect();
    try {
        await client.query("BEGIN");
        const result = await client.query("INSERT INTO orders (user_id, product, quantity) VALUES ($1, $2, $3) RETURNING id, user_id, product, quantity, status, created_at", [req.user.sub, product.trim(), quantity]);
        const order = result.rows[0];
        await client.query("COMMIT");
        await redis.del(`orders:user:${req.user.sub}`).catch(() => {});

        await fetch(`${notificationsUrl}/notifications`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ orderId: order.id, type: "order-created", message: `Order #${order.id} confirmed` })
        });
        return res.status(201).json(order);
    } catch (error) {
        await client.query("ROLLBACK").catch(() => {});
        console.error(error);
        return res.status(500).json({ error: "Unable to create order" });
    } finally {
        client.release();
    }
});

app.delete("/orders/:id", requireAuth, async (req, res) => {
    try {
        const result = await pool.query("DELETE FROM orders WHERE id = $1 AND user_id = $2 RETURNING id", [req.params.id, req.user.sub]);
        if (!result.rows[0]) return res.status(404).json({ error: "Order not found" });
        await redis.del(`orders:user:${req.user.sub}`).catch(() => {});
        return res.status(204).send();
    } catch (error) {
        return res.status(500).json({ error: "Unable to delete order" });
    }
});

app.get("/test-notification", async (req, res) => {
    try {
        const response = await fetch(`${notificationsUrl}/notifications`);

        const data = await response.json();

        res.json({
            service: "orders-service",
            notificationService: data
        });
    } catch (error) {
        res.status(500).json({
            error: "Unable to reach notifications-service",
            details: error.message
        });
    }
});

app.listen(PORT, "0.0.0.0", () => {
    console.log(`Orders service listening on port ${PORT}`);
});