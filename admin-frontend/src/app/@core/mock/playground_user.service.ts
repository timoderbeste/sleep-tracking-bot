import { of as observableOf,  Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import { PlaygroundUser, PlaygroundUserData } from '../data/playground_users';


@Injectable()
export class PlaygroundUserService extends PlaygroundUserData {

  constructor(private http: HttpClient) {
    super();
  }

  getUsers(): Observable<PlaygroundUser[]> {
    return this.http
      .get('http://localhost:4200/api/users')
      .map(this.extractPlaygroundUsers)
      .catch(this.handleErrorObservable);
  }

  private extractPlaygroundUsers(res: any) {
    console.log(res);
    return res.users.map(item => {
      return new PlaygroundUser(
        item.id,
        item.name,
        item.phone_number,
        item.country_code,
        item.email,
      );
    });
  }

  private handleErrorObservable(error: Response | any) {
    console.error(error.message || error);
    return Observable.throw(error.message || error);
  }
}
