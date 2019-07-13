import { NgModule } from '@angular/core';
import { Ng2SmartTableModule } from 'ng2-smart-table';

import { EmileComponent } from './emile.component';
import { EmileUserTableComponent } from './emile-user-table/emile-user-table.component';

@NgModule({
  imports: [
    Ng2SmartTableModule,
  ],
  declarations: [
    EmileComponent,
    EmileUserTableComponent,
  ],
  providers: [
  ],
})
export class EmileModule { }
