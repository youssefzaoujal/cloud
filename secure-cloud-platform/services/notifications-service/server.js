const express = require("express");
const cors = require("cors");
const helmet = require("helmet");
const rateLimit = require("express-rate-limit");
const { Pool } = require("pg");

const app = express();
const PORT = process.env.PORT || 3002;
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(rateLimit({ windowMs: 15 * 60 * 1000, limit: 100 }));

app.get("/health", (req, res) => {
    res.json({
        service: "notifications-service",
        status: "healthy"
    });
});

app.get("/notifications", async (req, res) => {
    try {
        const result = await pool.query("SELECT id, order_id, type, message, created_at FROM notifications ORDER BY created_at DESC");
        return res.json({ service: "notifications-service", notifications: result.rows });
    } catch (error) {
        console.error(error);
        return res.status(500).json({ error: "Unable to retrieve notifications" });
    }
});

app.post("/notifications", async (req, res) => {
    const { orderId, type, message } = req.body;
    if (!Number.isInteger(orderId) || typeof type !== "string" || typeof message !== "string" || !message.trim()) {
        return res.status(400).json({ error: "orderId, type, and message are required" });
    }

    try {
        const result = await pool.query("INSERT INTO notifications (order_id, type, message) VALUES ($1, $2, $3) RETURNING id, order_id, type, message, created_at", [orderId, type, message.trim()]);
        return res.status(201).json(result.rows[0]);
    } catch (error) {
        console.error(error);
        return res.status(500).json({ error: "Unable to create notification" });
    }
});

app.listen(PORT, "0.0.0.0", () => {
    console.log(`Notifications service listening on port ${PORT}`);
});