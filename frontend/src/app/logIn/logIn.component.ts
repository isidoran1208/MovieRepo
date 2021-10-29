import { HttpClient } from "@angular/common/http";
import { Component } from "@angular/core";
import { Router } from "@angular/router";
import { User } from "../model/user.model";

@Component({
  selector: 'app-login',
  templateUrl: './logIn.component.html',
})
export class LogInComponent{
    user: User = new User;

    constructor(private http: HttpClient, private router: Router) {}

    ngOnInit() {
      if (localStorage.getItem('token') != null){
        alert("User already logged in!");
        this.router.navigate(['/movies']);
      }   
    }

    onLogIn() {
      this.http.post("http://127.0.0.1:8000/api/token/", this.user)
      .subscribe((responseData: any) => {
        localStorage.setItem('user_id', this.parseJwt(responseData.access).user_id);
        localStorage.setItem('token', responseData.access);
        window.location.href="http://localhost:4200/movies/";
      });
    }

    parseJwt = (token) => {
      try {
        return JSON.parse(atob(token.split('.')[1]));
      } catch (e) {
        return null;
      }
    };
}