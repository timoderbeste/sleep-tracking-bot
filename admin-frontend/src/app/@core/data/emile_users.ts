import { Observable } from 'rxjs';

export class EmileUser {
  id: number;
  userName: string;
  phone: string;
  // timezone: string;
  // idealBedtime: string;
  // currentBedtime: string;
  // currentState: string;
  // weeklyPlanId: number;
  // weeklyHit: number;
  // weeklyMiss: number;

  constructor(
    id: number,
    userName: string,
    phone: string) {
      this.id = id;
      this.userName = userName;
      this.phone = phone;
  }
}

export abstract class EmileUserData {
  abstract getUsers(): Observable<EmileUser[]>;
  abstract createUser(data: Object): Observable<EmileUser>;
  abstract deleteUser(id: number): Observable<EmileUser>;
  abstract updateUser(id: number, data: Object): Observable<EmileUser>;
}
