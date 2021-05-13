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
            "time": Date.now().toString(),
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

function validateEmail() {
   var emailID = document.getElementById('email').value;
   atpos = emailID.indexOf("@");
   dotpos = emailID.lastIndexOf(".");

   if (atpos < 1 || ( dotpos - atpos < 2 )) {
      alert("Please enter correct email ID")
      document.getElementById('email').focus() ;
      return false;
   }
   return( true );
}

function validateCourse() {
  var course_pattern = new RegExp("^[A-z]{2}[0-9]{3}$", "m");
  if (course_pattern.test(document.getElementById('course').value) == false) {
    alert("Please enter a correct course code");
    document.getElementById('course').focus() ;
    return false;
  } else {
    return true;
  };
}

function validateInputs() {
  validateEmail() && validateCourse() ? createItem(): document.getElementById('textarea').innerHTML = "try again";
  return


}
