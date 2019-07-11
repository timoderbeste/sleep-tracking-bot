import { Observable } from 'rxjs';

export class PlaygroundUser {
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

export abstract class PlaygroundUserData {
  abstract getUsers(): Observable<PlaygroundUser[]>;
  abstract createUser(data: Object): Observable<PlaygroundUser>;
  abstract deleteUser(id: number): Observable<PlaygroundUser>;
  abstract updateUser(id: number, data: Object): Observable<PlaygroundUser>;
}
