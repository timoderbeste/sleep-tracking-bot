import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import { EmileRecord, EmileRecordData } from '../data/emile-record';


@Injectable()
export class EmileRecordService extends EmileRecordData {

  constructor(private http: HttpClient) {
    super();
  }

  getAll(): Observable<EmileRecord[]> {
    // TODO: Use the correct api to get all records
    return this.http
        .get('http://localhost:5001/api/records/')
        .map(this.extractAll)
        .catch(this.handleErrorObservable);
  }

  createOne(data: Object): Observable<EmileRecord> {
    // TODO: Use the correct api to create a record
    const headers = new HttpHeaders({'Content-Type': 'application/json'});
    const options = {headers: headers};
    return this.http.post('http://localhost:5001/api/records/', data, options)
        .map(this.extractOne)
        .catch(this.handleErrorObservable);
  }

  deleteOne(id: number): Observable<EmileRecord> {
    // TODO: Use the correct api to delete a record
    return this.http.delete(`http://localhost:5001/api/records/${id}`)
        .map(this.extractOne)
        .catch(this.handleErrorObservable);
  }

  updateOne(id: number, data: Object): Observable<EmileRecord> {
    // TODO: Use the correct api to update a record
    const headers = new HttpHeaders({'Content-Type': 'application/json'});
    const options = {headers: headers};
    return this.http.put(`http://localhost:5001/api/records/${id}`, data, options)
        .map(this.extractOne)
        .catch(this.handleErrorObservable);
  }

  private extractAll(res: any) {
    console.log(res);
    return res.records.map(item => {
      return new EmileRecord(
        item.id,
        item.isSlept,
        item.reason,
        item.userId,
        item.weeklyPlanId,
        item.date,
      );
    });
  }

  private extractOne(res: any): EmileRecord {
    const item = res.record;
    return new EmileRecord(
      item.id,
      item.isSlept,
      item.reason,
      item.userId,
      item.weeklyPlanId,
      item.date,
    );
  }

  private handleErrorObservable(error: Response | any) {
    console.error(error.message || error);
    return Observable.throw(error.message || error);
  }
}
