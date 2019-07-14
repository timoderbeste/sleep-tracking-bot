import { Observable } from 'rxjs';

export class EmilePlan {
  id: number;
  weeklyBedtime: string;
  weeklyFrequency: string;

  constructor(
    id: number,
    weeklyBedtime: string,
    weeklyFrequency: string) {
      this.id = id;
      this.weeklyBedtime = weeklyBedtime;
      this.weeklyFrequency = weeklyFrequency;
  }
}

export abstract class EmilePlanData {
  abstract getAll(): Observable<EmilePlan[]>;
  abstract createOne(data: Object): Observable<EmilePlan>;
  abstract deleteOne(id: number): Observable<EmilePlan>;
  abstract updateOne(id: number, data: Object): Observable<EmilePlan>;
}
