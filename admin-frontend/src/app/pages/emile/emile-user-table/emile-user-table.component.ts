import { Component, OnInit } from '@angular/core';
import { LocalDataSource } from 'ng2-smart-table';

import { EmileUser, EmileUserData } from '../../../@core/data/emile_users';


@Component({
  selector: 'ngx-emile-user-table',
  templateUrl: './emile-user-table.component.html',
})
export class EmileUserTableComponent implements OnInit {

  userSource: LocalDataSource;

  smartTableSettings = {
    columns: {
      id: {
        title: 'ID',
        isEditable: false,
      },
      userName: {
        title: 'Full Name',
      },
      phone: {
        title: 'Phone Number',
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

  constructor(private emileUserService: EmileUserData) { }

  ngOnInit() {
    this.getUsers();
  }

  getUsers() {
    this.emileUserService.getUsers()
        .subscribe((users: [EmileUser]) => {
          console.log('users:', users);
          const jsonifiedUsers = users.map(item => {
            return {
              'id': item.id,
              'userName': item.userName,
              'phone': item.phone,
            };
          });
          this.userSource = new LocalDataSource(jsonifiedUsers);
        });
  }

  createUser(event) {
    console.log(event);
    if (window.confirm('Are you sure you want to create?')) {
      this.emileUserService.createUser(event.newData)
          .subscribe((user: EmileUser) => {
            console.log(user);
            this.getUsers();
            event.confirm.resolve();
          });
    } else {
      event.confirm.reject();
    }
  }

  deleteUser(event) {
    console.log(event);
    if (window.confirm('Are you sure you want to delete?')) {
      this.emileUserService.deleteUser(event.data.id)
          .subscribe((user: EmileUser) => {
            console.log('user deleted:', user);
            this.getUsers();
            event.confirm.resolve();
          });
    } else {
      event.confirm.reject();
    }
  }

  editUser(event) {
    console.log('editUser event', event);
    if (window.confirm('Are you sure you want to update?')) {
      this.emileUserService.updateUser(event.newData.id, event.newData)
          .subscribe((user: EmileUser) => {
            console.log('user updated:', user);
            this.getUsers();
            event.confirm.resolve();
          });
    } else {
      event.confirm.reject();
    }
  }

}
