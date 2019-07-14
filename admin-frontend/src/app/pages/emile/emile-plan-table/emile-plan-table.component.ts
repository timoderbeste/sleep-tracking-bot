import { Component, OnInit } from '@angular/core';
import { LocalDataSource } from 'ng2-smart-table';

import { EmilePlan, EmilePlanData } from '../../../@core/data/emile-plan';


@Component({
  selector: 'ngx-emile-plan-table',
  templateUrl: './emile-plan-table.component.html',
})
export class EmilePlanTableComponent implements OnInit {

  planSource: LocalDataSource;

  smartTableSettings = {
    columns: {
      id: {
        title: 'Plan Id',
        isEditable: false,
      },
      weeklyBedtime: {
        title: 'Weekly Bedtime',
      },
      weeklyFrequency: {
        title: 'Weekly Frequency',
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

  constructor(private emilePlanService: EmilePlanData) { }

  ngOnInit() {
    this.getPlans();
  }

  getPlans() {
    this.emilePlanService.getAll()
        .subscribe((plans: [EmilePlan]) => {
          console.log('plans:', plans);
          const jsonifiedPlans = plans.map(item => {
            return {
              'id': item.id,
              'weeklyFrequency': item.weeklyFrequency,
              'weeklyBedtime': item.weeklyBedtime,
            };
          });
          this.planSource = new LocalDataSource(jsonifiedPlans);
        });
  }

  createPlan(event) {
    console.log(event);
    if (window.confirm('Are you sure you want to create?')) {
      this.emilePlanService.createOne(event.newData)
          .subscribe((plan: EmilePlan) => {
            console.log(plan);
            this.getPlans();
            event.confirm.resolve();
          });
    } else {
      event.confirm.reject();
    }
  }

  deletePlan(event) {
    console.log(event);
    if (window.confirm('Are you sure you want to delete?')) {
      this.emilePlanService.deleteOne(event.data.id)
          .subscribe((plan: EmilePlan) => {
            console.log('plan deleted:', plan);
            this.getPlans();
            event.confirm.resolve();
          });
    } else {
      event.confirm.reject();
    }
  }

  editPlan(event) {
    console.log('editPlan event', event);
    if (window.confirm('Are you sure you want to update?')) {
      this.emilePlanService.updateOne(event.newData.id, event.newData)
          .subscribe((plan: EmilePlan) => {
            console.log('plan updated:', plan);
            this.getPlans();
            event.confirm.resolve();
          });
    } else {
      event.confirm.reject();
    }
  }

}
