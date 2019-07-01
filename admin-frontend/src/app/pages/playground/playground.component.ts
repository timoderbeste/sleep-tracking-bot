import { Component, OnInit } from '@angular/core';

import { PlaygroundUser, PlaygroundUserData } from '../../@core/data/playground_users';

@Component({
  selector: 'ngx-playground',
  templateUrl: './playground.component.html',
})
export class PlaygroundComponent implements OnInit {

  users: any;
  jsonifiedUsers: any;

  smartTableSettings = {
    columns: {
      id: {
        title: 'ID'
      },
      name: {
        title: 'Full Name'
      },
      phoneNumber: {
        title: 'Phone Number'
      },
      countryCode: {
        title: 'Country Code'
      },
      email: {
        title: 'Email'
      }
    }
  };

  constructor(private playgroundUserService: PlaygroundUserData) { }

  ngOnInit() {
    this.playgroundUserService.getUsers()
    .subscribe((users: [PlaygroundUser]) => {
      this.users = users;
      this.jsonifyUsers();

      console.log(this.jsonifiedUsers);
    });
  }

  jsonifyUsers() {
    this.jsonifiedUsers = this.users.map(item => {
      return {
        'id': item.id,
        'name': item.name,
        'phoneNumber': item.phone_number,
        'countryCode': item.country_code,
        'email': item.email,
      }
    });
  }

}
