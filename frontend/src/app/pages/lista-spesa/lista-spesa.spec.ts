import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListaSpesa } from './lista-spesa';

describe('ListaSpesa', () => {
  let component: ListaSpesa;
  let fixture: ComponentFixture<ListaSpesa>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListaSpesa],
    }).compileComponents();

    fixture = TestBed.createComponent(ListaSpesa);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
