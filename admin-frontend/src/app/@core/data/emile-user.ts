import { Observable } from 'rxjs';

export class EmileUser {
  id: number;
  userName: string;
  phone: string;
  timezone: string;
  idealBedtime: string;
  currentBedtime: string;
  currentState: string;
  weeklyPlanId: number;
  weeklyHit: number;
  weeklyMiss: number;

  constructor(
    id: number,
    userName: string,
    phone: string,
    timezone: string,
    idealBedtime: string,
    currentBedtime: string,
    currentState: string,
    weeklyPlanId: number,
    weeklyHit: number,
    weeklyMiss: number,
  ) {
      this.id = id;
      this.userName = userName;
      this.phone = phone;
      this.timezone = timezone;
      this.idealBedtime = idealBedtime;
      this.currentBedtime = currentBedtime;
      this.currentState = currentState;
      this.weeklyPlanId = weeklyPlanId;
      this.weeklyHit = weeklyHit;
      this.weeklyMiss = weeklyMiss;
  }
}

export abstract class EmileUserData {
  abstract getAll(): Observable<EmileUser[]>;
  abstract createOne(data: Object): Observable<EmileUser>;
  abstract deleteOne(id: number): Observable<EmileUser>;
  abstract updateOne(id: number, data: Object): Observable<EmileUser>;
}
