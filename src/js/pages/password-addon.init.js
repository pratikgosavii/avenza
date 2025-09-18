/*
Template Name: Doot - Responsive Bootstrap 5 Chat App
Author: Pichforest
Website: https://Pichforest.com/
Contact: Pichforest@gmail.com
File: password addon Js File
*/

// password addon
document.getElementById('password-addon').addEventListener('click', function () {
	var passwordInput = document.getElementById("password-input");
	if (passwordInput.type === "password") {
		passwordInput.type = "text";
	} else {
		passwordInput.type = "password";
	}
});
