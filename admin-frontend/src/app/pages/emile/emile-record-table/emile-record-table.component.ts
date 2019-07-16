import { Component, OnInit } from '@angular/core';
import { LocalDataSource } from 'ng2-smart-table';

import { EmileRecord, EmileRecordData } from '../../../@core/data/emile-record';

@Component({
  selector: 'ngx-emile-record-table',
  templateUrl: './emile-record-table.component.html',
})
export class EmileRecordTableComponent implements OnInit {

  recordSource: LocalDataSource;

  smartTableSettings = {
    columns: {
      id: {
        title: 'Record Id',
        isEditable: false,
      },
      reason: {
        title: 'Reason',
      },
      isSlept: {
        title: 'Slept',
      },
      date: {
        title: 'Date',
      },
      userId: {
        title: 'User Id',
      },
      weeklyPlanId: {
        title: 'Weekly Plan Id',
      },
    },
    add: {
      addButtonContent: '<i class="nb-plus"></i>',
      createButtonContent: '<i class="nb-checkmark"></i>',
      cancelButtonContent: '<i class="nb-close"></i>',
      confirmCreate: true,
    },
    edit: {
      editButtonContent: '<i class="nb-edit"></i>',
      saveButtonContent: '<i class="nb-checkmark"></i>',
      cancelButtonContent: '<i class="nb-close"></i>',
      confirmSave: true,
    },
    delete: {
      deleteButtonContent: '<i class="nb-trash"></i>',
      confirmDelete: true,
    },
    mode: 'inline',
  };

  constructor(private emileRecordService: EmileRecordData) { }

  ngOnInit() {
    this.getRecords();
  }

  getRecords() {
    this.emileRecordService.getAll()
        .subscribe((records: [EmileRecord]) => {
          console.log('records:', records);
          const jsonifiedRecords = records.map(item => {
            return {
              'id': item.id,
              'isSlept': item.isSlept,
              'reason': item.reason,
              'userId': item.userId,
              'weeklyPlanId': item.weeklyPlanId,
              'date': item.date,
            };
          });
          this.recordSource = new LocalDataSource(jsonifiedRecords);
        });
  }

  createRecord(event) {
    console.log(event);
    if (window.confirm('Are you sure you want to create?')) {
      this.emileRecordService.createOne(event.newData)
          .subscribe((record: EmileRecord) => {
            console.log(record);
            this.getRecords();
            event.confirm.resolve();
          });
    } else {
      event.confirm.reject();
    }
  }

  deleteRecord(event) {
    console.log(event);
    if (window.confirm('Are you sure you want to delete?')) {
      this.emileRecordService.deleteOne(event.data.id)
          .subscribe((record: EmileRecord) => {
            console.log('record deleted:', record);
            this.getRecords();
            event.confirm.resolve();
          });
    } else {
      event.confirm.reject();
    }
  }

  editRecord(event) {
    console.log('editRecord event', event);
    if (window.confirm('Are you sure you want to update?')) {
      this.emileRecordService.updateOne(event.newData.id, event.newData)
          .subscribe((record: EmileRecord) => {
            console.log('record updated:', record);
            this.getRecords();
            event.confirm.resolve();
          });
    } else {
      event.confirm.reject();
    }
  }

}
