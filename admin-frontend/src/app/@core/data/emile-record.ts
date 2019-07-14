import { Observable } from 'rxjs';

export class EmileRecord {
  id: number;
  isSlept: boolean;
  reason: string;
  userId: number;
  weeklyPlanId: number;
  date: string;

  constructor(
    id: number,
    isSlept: boolean,
    reason: string,
    userId: number,
    weeklyPlanId: number,
    date: string,
  ) {
      this.id = id;
      this.isSlept = isSlept;
      this.reason = reason;
      this.userId = userId;
      this.weeklyPlanId = weeklyPlanId;
      this.date = date;
  }
}

export abstract class EmileRecordData {
  abstract getAll(): Observable<EmileRecord[]>;
  abstract createOne(data: Object): Observable<EmileRecord>;
  abstract deleteOne(id: number): Observable<EmileRecord>;
  abstract updateOne(id: number, data: Object): Observable<EmileRecord>;
}
