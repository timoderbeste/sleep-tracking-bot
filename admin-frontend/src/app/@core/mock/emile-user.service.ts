import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import { EmileUser, EmileUserData } from '../data/emile-user';


@Injectable()
export class EmileUserService extends EmileUserData {

  constructor(private http: HttpClient) {
    super();
  }

  getAll(): Observable<EmileUser[]> {
    return this.http
        .get('http://localhost:5001/api/users/')
        .map(this.extractAll)
        .catch(this.handleErrorObservable);
  }

  createOne(data: Object): Observable<EmileUser> {
    const headers = new HttpHeaders({'Content-Type': 'application/json'});
    const options = {headers: headers};
    return this.http.post('http://localhost:5001/api/users/', data, options)
        .map(this.extractOne)
        .catch(this.handleErrorObservable);
  }

  deleteOne(id: number): Observable<EmileUser> {
    return this.http.delete(`http://localhost:5001/api/users/${id}`)
        .map(this.extractOne)
        .catch(this.handleErrorObservable);
  }

  updateOne(id: number, data: Object): Observable<EmileUser> {
    const headers = new HttpHeaders({'Content-Type': 'application/json'});
    const options = {headers: headers};
    return this.http.put(`http://localhost:5001/api/users/${id}`, data, options)
        .map(this.extractOne)
        .catch(this.handleErrorObservable);
  }

  private extractAll(res: any) {
    console.log(res);
    return res.users.map(item => {
      return new EmileUser(
        item.id,
        item.userName,
        item.phone,
        item.timezone,
        item.idealBedtime,
        item.currentBedtime,
        item.currentState,
        item.weeklyPlanId,
        item.weeklyHit,
        item.weeklyMiss,
      );
    });
  }

  private extractOne(res: any): EmileUser {
    const item = res.user;
    return new EmileUser(
      item.id,
      item.userName,
      item.phone,
      item.timezone,
      item.idealBedtime,
      item.currentBedtime,
      item.currentState,
      item.weeklyPlanId,
      item.weeklyHit,
      item.weeklyMiss,
    );
  }

  private handleErrorObservable(error: Response | any) {
    console.error(error.message || error);
    return Observable.throw(error.message || error);
  }
}
