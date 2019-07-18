import {CommonModule} from '@angular/common';
import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {RouterModule} from '@angular/router';

import {NgxAuthRoutingModule} from './auth-routing.module';
import {NbAuthJWTToken, NbAuthModule, NbPasswordAuthStrategy} from '@nebular/auth';
import {NgxLoginComponent} from './login/login.component';
import {CookieService} from 'ngx-cookie-service';
import {
  NbAlertModule,
  NbButtonModule,
  NbCheckboxModule,
  NbInputModule,
} from '@nebular/theme';
import {UserService} from '../../@core/mock/users.service';


@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    NbAlertModule,
    NbInputModule,
    NbButtonModule,
    NbCheckboxModule,
    NgxAuthRoutingModule,
    NbAuthModule,
    NbAuthModule.forRoot({
      strategies: [
        NbPasswordAuthStrategy.setup({
          name: 'account',
          baseEndpoint: 'http://127.0.0.1:5001/api/auth',
          login: {
            endpoint: '/login',
            method: 'post',
          },
        }),
      ],
      forms: {},
    }),
  ],
  declarations: [
    NgxLoginComponent,
  ],
  providers: [
    CookieService,
    UserService,
  ],
})
export class NgxAuthModule {
}
