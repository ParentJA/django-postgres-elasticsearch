/// <reference types="cypress" />

describe('Perusable', function () {
  it('Displays the home page.', function () {
    cy.visit('/');
    cy.get('h1').should('contain', 'Perusable');
  });

  it('Displays a list of results.', function () {
    // cy.intercept('GET', '**/api/v1/catalog/wines/**', { fixture: 'wines.json' }).as('getWines');
    cy.intercept('GET', '**/api/v1/catalog/wines/**').as('getWines');

    cy.visit('/');
    cy.get('input[placeholder="Enter a search term (e.g. cabernet)"]')
      .type('cabernet');
    cy.get('button').contains('Search').click();
    cy.wait('@getWines');
    cy.get('div.card-title').should('contain', 'Cabernet Sauvignon');
  });

  it('Displays wine search words.', function () {
    // cy.intercept(
    //   'GET', '**/api/v1/catalog/wine-search-words/**',
    //   { fixture: 'wine_search_words.json' }
    // ).as('getWineSearchWords');
    cy.intercept('GET', '**/api/v1/catalog/wine-search-words/**').as('getWineSearchWords');

    cy.visit('/');
    cy.get('input[placeholder="Enter a search term (e.g. cabernet)"]')
      .type('cabarnet');
    cy.wait('@getWineSearchWords');
    cy.get('div#query').should('contain', 'cabernet');
  });
});
