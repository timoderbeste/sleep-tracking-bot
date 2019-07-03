import { Observable } from 'rxjs';

export class PlaygroundUser {
  id: number;
  userName: string;
  phone: string;
  currentPlan: string;
  personalInformation: string;
  // name: string;
  // phone_number: string;
  // country_code: string;
  // email: string;

  constructor(
    id: number,
    userName: string,
    phone: string,
    currentPlan: string,
    personalInformation: string
    // name: string,
    // phone_number: string,
    // country_code: string,
    // email: string
  ) {
    this.id = id;
    this.userName = userName;
    this.phone = phone;
    this.currentPlan = currentPlan;
    this.personalInformation = personalInformation;
    // this.name = name;
    // this.phone_number = phone_number;
    // this.country_code = country_code;
    // this.email = email;
  }
}

export abstract class PlaygroundUserData {
  abstract getUsers(): Observable<PlaygroundUser[]>;
  abstract createUser(data: Object): Observable<PlaygroundUser>;
  abstract deleteUser(id: number): Observable<PlaygroundUser>;
  abstract updateUser(id: number, data: Object): Observable<PlaygroundUser>;
}
