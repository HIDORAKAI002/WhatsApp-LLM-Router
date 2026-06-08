const express = require('express');
const config = require('./config/env');
const webhookRoutes = require('./routes/webhook_routes');
const whatsappClient = require('./core/whatsapp_client');

const app = express();
app.use(express.json());

// Register routes
app.use('/', webhookRoutes);

// Start Express Server
app.listen(config.PORT, () => {
    console.log(`========================================`);
    console.log(`🚀 Text Agent VPS Server is RUNNING`);
    console.log(`📡 Listening on Port: ${config.PORT}`);
    console.log(`🧠 Brain Server URL: ${config.BRAIN_SERVER_URL}`);
    console.log(`========================================\n`);
    
    // Start WhatsApp Client
    whatsappClient.start();
});
