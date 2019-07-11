import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

import { NgxAuthRoutingModule } from './auth-routing.module';
import { NbAuthModule, NbPasswordAuthStrategy} from '@nebular/auth';
import { NgxLoginComponent } from './login/login.component'; // <---
import {
    NbAlertModule,
    NbButtonModule,
    NbCheckboxModule,
    NbInputModule,
} from '@nebular/theme';


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
                    baseEndpoint: 'http://127.0.0.1:5000/api/auth',
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
})
export class NgxAuthModule {
}
