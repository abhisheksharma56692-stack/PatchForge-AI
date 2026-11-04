/**
 * Intentionally vulnerable Express.js application for testing CWE-22 (Path Traversal)
 */
const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PUBLIC_DIR = path.join(__dirname, 'public');

app.get('/download', (req, res) => {
    const filename = req.query.file;
    // Vulnerable sink: Directly resolving untrusted filename (CWE-22)
    const filePath = path.join(PUBLIC_DIR, filename);
    
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            return res.status(404).send('File not found');
        }
        res.send(data);
    });
});

app.listen(3000, () => {
    console.log('Vulnerable Express app listening on port 3000');
});

