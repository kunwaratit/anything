function Validation(values) {
  let error = {};
  const email_pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const password_pattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,15}$/;

  if (values.first_name === "") {
    error.first_name = "Naaame should not be empty";
  } else {
    error.name = "";
  }
  if (values.phone_number === "") {
    error.phone_number = "Phone number should not be empty";
  }
   else if (!/^\d{10}$/.test(values.phone_number)) {
    error.phone_number = "Phone number must be 10 digits long";
  } else {
    error.phone_number = "";
  }
  if (values.email === "") {
    error.email = "email should not be empty";
  } else if (email_pattern.test(values.email)) {
    error.email = "";
  } else {
    error.email = "email should be valid";
  }

  if (values.password === "") {
    error.password = "password should not be empty";
  }else if (values.password.length < 8) {
    error.password = "Password must be at least 8 characters long";
  }
  else if (password_pattern.test(values.password)) {
    error.password = "";
  }
   else {
    error.password =
      "passworld should contain at least one lowercase letter, one uppercase letter, one numeric digit, and one special character";
  }

  if (values.password !== values.confirmpassword) {
    error.confirmpassword = "Password Didn't Match";
  } else {
    error.confirmpassword = "";
  }
  return error;
}

export default Validation;
