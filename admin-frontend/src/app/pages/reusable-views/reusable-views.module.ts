import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Ng2SmartTableModule } from 'ng2-smart-table';
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';

import { NgxSmartTableDatepickerComponent } from './ngx-smart-table-datepicker/ngx-smart-table-datepicker.component';

@NgModule({
  imports: [
    Ng2SmartTableModule,
    OwlDateTimeModule,
    OwlNativeDateTimeModule,
    FormsModule
  ],
  declarations: [
    NgxSmartTableDatepickerComponent,
  ],
  providers: [
  ],
  entryComponents: [
  ],
})
export class ReusableViewsModule { }
