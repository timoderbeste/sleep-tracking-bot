import {ChangeDetectorRef, Component, Inject} from '@angular/core';
import {
  deepExtend, getDeepFromObject,
  NB_AUTH_OPTIONS, NbAuthJWTToken,
  NbAuthResult,
  NbAuthService,
  NbAuthSocialLink,
  NbLoginComponent,
} from '@nebular/auth';
import {Router} from '@angular/router';
import {HttpClient} from '@angular/common/http';
import * as JsEncryptModule from 'jsencrypt';
import {CookieService} from 'ngx-cookie-service';
import {UserData} from '../../../@core/data/users';

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

  publicKey: string;
  encryptedKey: string;

  constructor(protected service: NbAuthService,
              @Inject(NB_AUTH_OPTIONS) protected options = {},
              protected cookie: CookieService,
              protected cd: ChangeDetectorRef,
              private userService: UserData,
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
    if (cookie.get('isRemember') === 'true') {
      this.messages = ['Already logged in, redirecting...'];
      sessionStorage.setItem('isLoggedIn', 'true');
      setTimeout(() => {
        return this.router.navigateByUrl('/pages');
      }, this.redirectDelay);
    }
    this.user.rememberMe = false;
    this.getPublicKey();
  }

  getPublicKey() {
    this.httpClient.get('http://127.0.0.1:5001/api/auth/login').subscribe((data: { public_key: string }) => {
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
      const responseBody = result.getResponse()['body'];
      if (responseBody['login_status'] === 'success') {
        this.messages = responseBody['messages'];
        this.userService.setUser(responseBody['username'], {
          name: responseBody['username'],
          picture: responseBody['picture'],
        });
        this.user.name = responseBody['username'];
        if (this.user.rememberMe === true) {
          this.cookie.set('isRemember', 'true');
        } else {
          this.cookie.set('isRemember', 'false');
        }
        sessionStorage.setItem('isLoggedIn', 'true');
        sessionStorage.setItem('currUser', responseBody['username']);
      } else {
        this.errors = responseBody['errors'];
        this.user.password = '';
      }

      const redirect = responseBody['redirect'];
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
