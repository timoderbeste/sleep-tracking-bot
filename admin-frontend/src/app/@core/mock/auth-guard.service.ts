import {Injectable, NgModule} from '@angular/core';
import {CanActivate, Router} from '@angular/router';
import { NbAuthService } from '@nebular/auth';
import {tap} from 'rxjs/operators';
import {CookieService} from 'ngx-cookie-service';


@Injectable()
export class AuthGuard implements CanActivate {

  constructor(private authService: NbAuthService,
              private router: Router,
              protected cookie: CookieService) {
  }

  canActivate() {
    if (sessionStorage.getItem('isLoggedIn') === 'true') {
      return true;
    } else {
      this.router.navigate(['auth/login']);
      return false;
    }
  }
}
