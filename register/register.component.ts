import { Component, OnInit } from '@angular/core';
import { UserserviceService } from '../userservice.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  //message:any="";
  user: any;
  registerForm: FormGroup;
  submitted = false;
  msg: any;
  

  constructor(private router: Router, private service: UserserviceService) {
    this.user = { loginId: '', email: '', password: '' };
  }

  ngOnInit(): void {
    this.service.getAllUsers().subscribe((result: any) => { console.log(result); this.users = result; });
    this.registerForm = this.formBuilder.group({
      loginId: ['', [Validators.required, Validators.minLength(5)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8), PasswordValidator.strong]],
      confirmPassword: ['', Validators.required]
    }, {
      validator: MustMatch('password', 'confirmPassword')
    });
    this.msg = JSON.parse(localStorage.getItem("msg"));
    if (this.msg) {
      this.toastr.error("Not Registered!!");
    }
    this.msg = "";
    localStorage.setItem('msg', JSON.stringify(''));

  }

  register(regForm: any) {
    if (regForm.password != regForm.password2) {
      this.toastr.error("Password not Matching");
    } else {
      this.service.registerUser(this.user).subscribe((result: any) => { console.log(this.user); });
      localStorage.setItem('msg', JSON.stringify('msg'));
      this.router.navigate(['login']);
    }
  }
  get f() { return this.registerForm.controls; }

  userNameTaken(): any {
    var searchText = this.registerForm.value.loginId;
    searchText = searchText.toLowerCase();
    return this.users.filter(item => {
      if (item && item['loginId']) {
        return item['loginId'].toLowerCase() === searchText;
      }
      return false;
    });
  }

  emailTaken(): any {
    var searchText = this.registerForm.value.email;
    searchText = searchText.toLowerCase();
    return this.users.filter(item => {
      if (item && item['email']) {
        return item['email'].toLowerCase() === searchText;
      }
      return false;
    });
  }

  onSubmit() {
    this.submitted = true;
    if (this.registerForm.invalid) {
      if (this.userNameTaken().length > 0) {
        this.taken = true;
        this.msg = this.user.loginId;
      }
      if (this.emailTaken().length > 0) {
        this.submitted = false;
        this.taken = false;
        this.toastr.warning("Account Exists with the mail, " + this.user.email);
        this.registerForm.reset();
      }
      return;
    }
    if (this.emailTaken().length > 0) {
      this.submitted = false;
      this.taken = false;
      this.msg.warning("Account Exists with the mail, " + this.user.email);
      this.registerForm.reset();
    }
    if (this.userNameTaken().length > 0) {
      this.taken = true;
      this.msg = this.user.loginId;
      console.log(this.userNameTaken());
      return;
    }
    this.service.sendMail(this.user.email, this.user.loginId).subscribe((result: any) => { console.log(result); this.otp = result });

    document.getElementById('id01').style.display = 'block';

  }
}