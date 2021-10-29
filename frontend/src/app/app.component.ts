import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  userLoggedIn: boolean;

  ngOnInit() {
    this.userLoggedIn = localStorage.getItem('token') != null;
  }
}
