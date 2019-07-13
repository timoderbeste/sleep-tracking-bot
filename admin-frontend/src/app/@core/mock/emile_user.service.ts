import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import { EmileUser, EmileUserData } from '../data/emile_users';


@Injectable()
export class EmileUserService extends EmileUserData {

  constructor(private http: HttpClient) {
    super();
  }

  getUsers(): Observable<EmileUser[]> {
    return this.http
        .get('http://localhost:5001/api/users/')
        .map(this.extractEmileUsers)
        .catch(this.handleErrorObservable);
  }

  createUser(data: Object): Observable<EmileUser> {
    const headers = new HttpHeaders({'Content-Type': 'application/json'});
    const options = {headers: headers};
    return this.http.post('http://localhost:5001/api/users/', data, options)
        .map(this.extractEmileUser)
        .catch(this.handleErrorObservable);
  }

  deleteUser(id: number): Observable<EmileUser> {
    return this.http.delete(`http://localhost:5001/api/users/${id}`)
        .map(this.extractEmileUser)
        .catch(this.handleErrorObservable);
  }

  updateUser(id: number, data: Object): Observable<EmileUser> {
    const headers = new HttpHeaders({'Content-Type': 'application/json'});
    const options = {headers: headers};
    return this.http.put(`http://localhost:5001/api/users/${id}`, data, options)
        .map(this.extractEmileUser)
        .catch(this.handleErrorObservable);
  }

  private extractEmileUsers(res: any) {
    console.log(res);
    return res.users.map(item => {
      return new EmileUser(
          item.id,
          item.userName,
          item.phone,
      );
    });
  }

  private extractEmileUser(res: any): EmileUser {
    const item = res.user;
    return new EmileUser(
        item.id,
        item.userName,
        item.phone,
    );
  }

  private handleErrorObservable(error: Response | any) {
    console.error(error.message || error);
    return Observable.throw(error.message || error);
  }
}
