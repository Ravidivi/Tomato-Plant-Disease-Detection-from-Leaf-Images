const express = require('express');
const app = express();

// Define a route to handle incoming HTTP requests
app.get('/hello', async (req, res) => {
    try {
        // Call the Python Lambda function using AWS SDK
        const AWS = require('aws-sdk');
        const lambda = new AWS.Lambda();
        const params = {
            FunctionName: 'YourPythonLambdaFunctionName',
            InvocationType: 'RequestResponse',
            Payload: JSON.stringify({ name: req.query.name || 'World' }),
        };

        const response = await lambda.invoke(params).promise();
        const responseBody = JSON.parse(response.Payload);

        res.json({ message: responseBody.message });
    } catch (error) {
        console.error('Error calling Lambda function:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Start the server
const port = 3000;
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
