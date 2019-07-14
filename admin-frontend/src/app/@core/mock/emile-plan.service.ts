import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import { EmilePlan, EmilePlanData } from '../data/emile-plan';


@Injectable()
export class EmilePlanService extends EmilePlanData {

  constructor(private http: HttpClient) {
    super();
  }

  getAll(): Observable<EmilePlan[]> {
    // TODO: Use the correct api to get plans
    return this.http
        .get('http://localhost:5001/api/plans/')
        .map(this.extractAll)
        .catch(this.handleErrorObservable);
  }

  createOne(data: Object): Observable<EmilePlan> {
    // TODO: Use the correct api to create a plan
    const headers = new HttpHeaders({'Content-Type': 'application/json'});
    const options = {headers: headers};
    return this.http.post('http://localhost:5001/api/plans/', data, options)
        .map(this.extractOne)
        .catch(this.handleErrorObservable);
  }

  deleteOne(id: number): Observable<EmilePlan> {
    // TODO: Use the correct api to delete a plan
    return this.http.delete(`http://localhost:5001/api/plans/${id}`)
        .map(this.extractOne)
        .catch(this.handleErrorObservable);
  }

  updateOne(id: number, data: Object): Observable<EmilePlan> {
    // TODO: Use the correct api to update a plan
    const headers = new HttpHeaders({'Content-Type': 'application/json'});
    const options = {headers: headers};
    return this.http.put(`http://localhost:5001/api/plans/${id}`, data, options)
        .map(this.extractOne)
        .catch(this.handleErrorObservable);
  }

  private extractAll(res: any) {
    console.log(res);
    return res.plans.map(item => {
      return new EmilePlan(
          item.id,
          item.weeklyBedtime,
          item.weeklyFrequency,
      );
    });
  }

  private extractOne(res: any): EmilePlan {
    const item = res.user;
    return new EmilePlan(
        item.id,
        item.weeklyBedtime,
        item.weeklyFrequency,
    );
  }

  private handleErrorObservable(error: Response | any) {
    console.error(error.message || error);
    return Observable.throw(error.message || error);
  }
}
