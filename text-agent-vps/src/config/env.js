require('dotenv').config();

module.exports = {
    PORT: process.env.PORT || 3000,
    BRAIN_SERVER_URL: process.env.BRAIN_SERVER_URL || 'http://localhost:8000',
};
