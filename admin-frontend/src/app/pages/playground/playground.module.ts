import { NgModule } from '@angular/core';
import { Ng2SmartTableModule } from 'ng2-smart-table';

import { PlaygroundComponent } from './playground.component';

@NgModule({
  imports: [
    Ng2SmartTableModule,
  ],
  declarations: [
    PlaygroundComponent,
  ],
  providers: [
  ],
})
export class PlaygroundModule { }
