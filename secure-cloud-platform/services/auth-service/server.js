const express = require("express");

const app = express();
const PORT = process.env.PORT || 3000;

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

app.listen(PORT, "0.0.0.0", () => {
    console.log(`Auth service listening on port ${PORT}`);
});