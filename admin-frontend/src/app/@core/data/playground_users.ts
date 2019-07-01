import { Observable } from 'rxjs';

export class PlaygroundUser {
  id: number;
  name: string;
  phone_number: string;
  country_code: string;
  email: string;

  constructor(
    id: number, name: string,
    phone_number: string, country_code: string, email: string) {
    this.id = id;
    this.name = name;
    this.phone_number = phone_number;
    this.country_code = country_code;
    this.email = email;
  }
}

export abstract class PlaygroundUserData {
  abstract getUsers(): Observable<PlaygroundUser[]>;
}
