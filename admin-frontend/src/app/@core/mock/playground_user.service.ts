import { of as observableOf,  Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
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

  createUser(data: Object): Observable<PlaygroundUser> {
    let headers = new HttpHeaders({'Content-Type': 'application/json'});
    let options = {headers: headers};
    return this.http.post('http://localhost:4200/api/users', data, options)
            .map(this.extractPlaygroundUser)
            .catch(this.handleErrorObservable);
  }

  deleteUser(id: number): Observable<PlaygroundUser> {
    return this.http.delete('http://localhost:4200/api/users/' + id)
    .map(this.extractPlaygroundUser)
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

  private extractPlaygroundUser(res: any): PlaygroundUser {
    let item = res.user;
    return new PlaygroundUser(
      item.id,
      item.name,
      item.phone_number,
      item.country_code,
      item.email,
    );
  }

  private handleErrorObservable(error: Response | any) {
    console.error(error.message || error);
    return Observable.throw(error.message || error);
  }
}
