const express = require("express");
const bcrypt = require("bcryptjs");
const cors = require("cors");
const helmet = require("helmet");
const rateLimit = require("express-rate-limit");
const jwt = require("jsonwebtoken");
const { Pool } = require("pg");

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || "local-development-jwt-secret-change-me";
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

app.use(helmet());
app.use(cors());
app.use(express.json({ limit: "10kb" }));
app.use(rateLimit({ windowMs: 15 * 60 * 1000, limit: 100 }));

app.get("/health", (req, res) => {
    res.json({
        service: "auth-service",
        status: "healthy"
    });
});

app.get("/", (req, res) => {
    res.json({
        service: "auth-service",
        message: "Authentication service is running"
    });
});

app.post("/auth/register", async (req, res) => {
    const { email, password } = req.body;

    if (typeof email !== "string" || !/^\S+@\S+\.\S+$/.test(email) || typeof password !== "string" || password.length < 8) {
        return res.status(400).json({ error: "A valid email and password of at least 8 characters are required" });
    }

    try {
        const passwordHash = await bcrypt.hash(password, 12);
        const result = await pool.query(
            "INSERT INTO users (email, password_hash) VALUES ($1, $2) RETURNING id, email, created_at",
            [email.toLowerCase(), passwordHash]
        );
        return res.status(201).json({ user: result.rows[0] });
    } catch (error) {
        if (error.code === "23505") {
            return res.status(409).json({ error: "Email already registered" });
        }
        console.error(error);
        return res.status(500).json({ error: "Unable to register user" });
    }
});

app.post("/auth/login", async (req, res) => {
    const { email, password } = req.body;

    if (typeof email !== "string" || typeof password !== "string") {
        return res.status(400).json({ error: "Email and password are required" });
    }

    try {
        const result = await pool.query("SELECT id, email, password_hash FROM users WHERE email = $1", [email.toLowerCase()]);
        const user = result.rows[0];
        if (!user || !(await bcrypt.compare(password, user.password_hash))) {
            return res.status(401).json({ error: "Invalid credentials" });
        }

        const token = jwt.sign({ sub: user.id, email: user.email }, JWT_SECRET, { expiresIn: "1h" });
        return res.json({ token, user: { id: user.id, email: user.email } });
    } catch (error) {
        console.error(error);
        return res.status(500).json({ error: "Unable to login" });
    }
});

app.get("/auth/validate", (req, res) => {
    const token = req.headers.authorization?.replace("Bearer ", "");
    if (!token) {
        return res.status(401).json({ error: "Bearer token required" });
    }

    try {
        return res.json({ valid: true, user: jwt.verify(token, JWT_SECRET) });
    } catch {
        return res.status(401).json({ error: "Invalid or expired token" });
    }
});

app.listen(PORT, "0.0.0.0", () => {
    console.log(`Auth service listening on port ${PORT}`);
});