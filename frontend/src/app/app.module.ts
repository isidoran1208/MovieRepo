import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppComponent } from './app.component';
import { LogInComponent } from './logIn/logIn.component';
import { MovieEditComponent } from './movie-edit/movie-edit.component';
import { MovieListComponent } from './movie-list/movie-list.component';
import { NavbarComponent } from './navbar/navbar.component';
import { JwtInterceptor } from './util/jwt-interceptor';
import { MovieItemComponent } from './movie-item/movie-item.component';

const appRoutes: Routes = [
    {path: 'login', component: LogInComponent},
    {path: 'movies', component: MovieListComponent},
    {path: 'movies/:id', component: MovieItemComponent},
    {path: 'addmovie', component: MovieEditComponent},
];

@NgModule({
  declarations: [
    AppComponent,
    LogInComponent,
    MovieEditComponent,
    MovieListComponent,
    MovieItemComponent,
    NavbarComponent,
  ],
  imports: [
    FormsModule,
    BrowserModule,
    RouterModule.forRoot(appRoutes),
    HttpClientModule
  ],
  exports: [
    RouterModule
  ],
  providers: [{ provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true }],
  bootstrap: [AppComponent]
})
export class AppModule { }
