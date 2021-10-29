import { Inject, Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor, HTTP_INTERCEPTORS } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable()
export class JwtInterceptor implements HttpInterceptor {

  constructor() { }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    let token = localStorage.getItem('token');
    
    if (token)
        request = this.setHeader(request, token);

    return next.handle(request);
  }

  private setHeader(request: HttpRequest<any>, token: string): HttpRequest<any> {
    request = request.clone({
        setHeaders: {
            Authorization: `Bearer ${token}`
          }
        });
    
        return request;
    }
}