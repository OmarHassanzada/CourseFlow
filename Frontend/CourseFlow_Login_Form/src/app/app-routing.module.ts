import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { RegistrationComponent } from './pages/registration/registration.component';

const routes: Routes = [{
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
},
  {
    path: 'login',
    component: LoginComponent

  },
  {
    path: 'register',
    component: RegistrationComponent
  }]

@NgModule({
  declarations: [],
  imports: [
    RouterModule.forRoot(routes)
  ],
  exports: [RouterModule]


})
export class AppRoutingModule { }