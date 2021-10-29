import { Component } from "@angular/core";

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
})
export class NavbarComponent{

  constructor() {}

  onLogOut() {
      localStorage.clear();
      window.location.href="http://localhost:4200/login/";
  }
}