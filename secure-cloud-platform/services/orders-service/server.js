const express = require("express");

const app = express();
const PORT = process.env.PORT || 3001;

app.use(express.json());

app.get("/health", (req, res) => {
    res.json({
        service: "orders-service",
        status: "healthy"
    });
});

app.get("/orders", (req, res) => {
    res.json({
        service: "orders-service",
        orders: [
            {
                id: 1,
                product: "Laptop",
                status: "confirmed"
            },
            {
                id: 2,
                product: "Phone",
                status: "pending"
            }
        ]
    });
});

app.get("/test-notification", async (req, res) => {
    try {
        const response = await fetch(
            "http://notifications-service:3002/notifications"
        );

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