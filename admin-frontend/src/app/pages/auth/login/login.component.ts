import {ChangeDetectorRef, Component, Inject} from '@angular/core';
import {NB_AUTH_OPTIONS, NbAuthResult, NbAuthService, NbAuthSocialLink, NbLoginComponent} from '@nebular/auth';
import {Router} from '@angular/router';
import {getDeepFromObject} from '@nebular/auth/helpers';
import { HttpClient } from '@angular/common/http';
import * as JsEncryptModule from 'jsencrypt';

@Component({
    selector: 'ngx-login',
    templateUrl: './login.component.html',
})
export class NgxLoginComponent extends NbLoginComponent {
    redirectDelay: number = 0;
    showMessages: any = {};
    strategy: string = '';

    errors: string[] = [];
    messages: string[] = [];
    user: any = {};
    submitted: boolean = false;
    socialLinks: NbAuthSocialLink[] = [];
    rememberMe = false;

    publicKey: string;
    encryptedKey: string;

    constructor(protected service: NbAuthService,
                @Inject(NB_AUTH_OPTIONS) protected options = {},
                protected cd: ChangeDetectorRef,
                protected router: Router,
                private httpClient: HttpClient) {
        super(service, options, cd, router);
        this.options['forms']['validation']['account'] = {
            'required': true,
        };
        this.options['forms']['validation']['password'] = {
            'required': true,
            'minLength': 4,
            'maxLength': 200,
        };
        this.options['forms']['login']['strategy'] = 'account';
        this.redirectDelay = this.getConfigValue('forms.login.redirectDelay');
        this.showMessages = this.getConfigValue('forms.login.showMessages');
        this.strategy = this.getConfigValue('forms.login.strategy');
        this.socialLinks = this.getConfigValue('forms.login.socialLinks');
        this.rememberMe = this.getConfigValue('forms.login.rememberMe');
        this.getPublicKey();
    }

    getPublicKey() {
        this.httpClient.get('http://127.0.0.1:5000/api/auth/login').subscribe((data: {public_key: string}) => {
            this.publicKey = data.public_key;
        });
    }

    login(): void {
        this.errors = [];
        this.messages = [];
        this.submitted = true;
        const jsEncrypt = new JsEncryptModule.JSEncrypt();
        jsEncrypt.setPublicKey(this.publicKey);
        this.user.password = jsEncrypt.encrypt(this.user.password);


        this.service.authenticate(this.strategy, this.user).subscribe((result: NbAuthResult) => {
            this.submitted = false;
            console.log(result);
            if (result.isSuccess()) {
                this.messages = result.getMessages();
            } else {
                this.errors = result.getErrors();
            }

            const redirect = result.getRedirect();
            if (redirect) {
                setTimeout(() => {
                    return this.router.navigateByUrl(redirect);
                }, this.redirectDelay);
            }
            this.cd.detectChanges();
        });
    }

    getConfigValue(key: string): any {
        return getDeepFromObject(this.options, key, null);
    }
}
