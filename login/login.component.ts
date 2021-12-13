import { Component, OnInit } from '@angular/core';
import { UserserviceService } from '../userservice.service';
import { Router } from '@angular/router';
import { HeaderComponent } from '../header/header.component';
 

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  msg: any = "";
  message: any = "";
  user2: any;

  constructor(private router: Router, private service: UserserviceService) {
    this.user2 = { loginId: '', email: '', password: '' };
  }

  ngOnInit(): void {
    
  }

  loginSubmit(loginForm: any): void {
    
      this.service.verifyLogin(loginForm.loginId).subscribe((result: any) => {
        console.log(result);
        this.message = result;
        if (this.message) {
          if (this.message.password === loginForm.password) {
            
            this.router.navigate(['UserPage']);
          } else {
            this.router.error("Invalid Credentials");
          }
        } else {
          this.router.navigate(['register']);
        }
      });
    
  }
  navigate(): any {
    this.router.navigate(['register']);
  }
}
