const express = require("express");

const app = express();
const PORT = process.env.PORT || 3002;

app.use(express.json());

app.get("/health", (req, res) => {
    res.json({
        service: "notifications-service",
        status: "healthy"
    });
});

app.get("/notifications", (req, res) => {
    res.json({
        service: "notifications-service",
        notifications: [
            {
                id: 1,
                type: "email",
                message: "Order confirmed"
            },
            {
                id: 2,
                type: "sms",
                message: "Your order is being processed"
            }
        ]
    });
});

app.listen(PORT, "0.0.0.0", () => {
    console.log(`Notifications service listening on port ${PORT}`);
});