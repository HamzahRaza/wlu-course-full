AWS.config.region = 'us-east-1'; // Region
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: 'us-east-1:ead344a6-7d0d-4b50-987f-a7e15e52a263',
});
var docClient = new AWS.DynamoDB.DocumentClient();

function createItem() {
    var params = {
        TableName :"wlu-course-full",
        Item:{
            "course": document.getElementById('course').value,
            "term": document.getElementById('term').value,
            "email": document.getElementById('email').value,
        }
    };
    docClient.put(params, function(err, data) {
        if (err) {
            document.getElementById('textarea').innerHTML = "Unable to add item: " + "\n" + JSON.stringify(err, undefined, 2);
        } else {
            document.getElementById('textarea').innerHTML = "submitted";
        }
    });
}
