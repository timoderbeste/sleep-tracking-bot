import { Component, OnInit } from '@angular/core';
import { LocalDataSource } from 'ng2-smart-table';

import { PlaygroundUser, PlaygroundUserData } from '../../@core/data/playground_users';


@Component({
  selector: 'ngx-playground',
  templateUrl: './playground.component.html',
})
export class PlaygroundComponent implements OnInit {

  userSource: LocalDataSource;

  smartTableSettings = {
    columns: {
      id: {
        title: 'ID',
      },
      userName: {
        title: 'User Name',
      },
      phone: {
        title: 'Phone',
      },
      currentPlan: {
        title: 'Current Plan',
      },
      personalInformation: {
        title: 'Personal Information',
      },
      // name: {
      //   title: 'Full Name',
      // },
      // phoneNumber: {
      //   title: 'Phone Number',
      // },
      // countryCode: {
      //   title: 'Country Code',
      // },
      // email: {
      //   title: 'Email',
      // },
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

  constructor(private playgroundUserService: PlaygroundUserData) { }

  ngOnInit() {
    this.getUsers();
  }

  getUsers() {
    this.playgroundUserService.getUsers()
    .subscribe((users: [PlaygroundUser]) => {
      console.log('users:', users);
      const jsonifiedUsers = users.map(item => {
        return {
          'id': item.id,
          'userName': item.userName,
          'phone': item.phone,
          'currentPlan': item.currentPlan,
          'personalInformation': item.personalInformation,
          // 'name': item.name,
          // 'phoneNumber': item.phone_number,
          // 'countryCode': item.country_code,
          // 'email': item.email,
        };
      });
      this.userSource = new LocalDataSource(jsonifiedUsers);
    });
  }

  createUser(event) {
    console.log(event);
    if (window.confirm('Are you sure you want to create?')) {
      this.playgroundUserService.createUser(event.newData)
      .subscribe((user: PlaygroundUser) => {
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
      this.playgroundUserService.deleteUser(event.data.id)
      .subscribe((user: PlaygroundUser) => {
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
      this.playgroundUserService.updateUser(event.newData.id, event.newData)
      .subscribe((user: PlaygroundUser) => {
        console.log('user updated:', user);
        this.getUsers();
        event.confirm.resolve();
      });
    } else {
      event.confirm.reject();
    }
  }
}
