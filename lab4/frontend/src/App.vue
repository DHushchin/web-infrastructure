<template>
  <div>
    <h1>SQL Books</h1>
    <input v-model="newSqlBook.title" placeholder="Book title">
    <input v-model="newSqlBook.genre" placeholder="Book genre">
    <button @click="createSqlBook">Add a SQL book</button>
    <div v-for="book in sqlBooks" :key="book.id">
      {{ book.id }} - {{ book.title }} - {{ book.genre }}
      <button @click="deleteSqlBook(book.id)">Delete</button>
    </div>

    <h1>NoSQL Books</h1>
    <input v-model="newNoSqlBook.title" placeholder="Book title">
    <input v-model="newNoSqlBook.genre" placeholder="Book genre">
    <button @click="createNoSqlBook">Add a NoSQL book</button>
    <div v-for="book in noSqlBooks" :key="book._id">
      {{ book._id }} - {{ book.title }} - {{ book.genre }}
      <button @click="deleteNoSqlBook(book._id)">Delete</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      newSqlBook: {
        title: '',
        genre: ''
      },
      newNoSqlBook: {
        title: '',
        genre: ''
      },
      sqlBooks: [],
      noSqlBooks: []
    }
  },
  methods: {
    async getBooksSql() {
      const response = await axios.get('http://localhost:8080/get-sql-library')
      this.sqlBooks = response.data
    },
    async createSqlBook() {
      await axios.post('http://localhost:8080/create-sql-book', this.newSqlBook)

      await this.getBooksSql()

      this.newSqlBook.title = ''
      this.newSqlBook.genre = ''
    },
    async deleteSqlBook(bookId) {
      await axios.delete('http://localhost:8080/delete-sql-book/' + bookId)

      await this.getBooksSql()
    },
    async getBooksNoSql() {
      const response = await axios.get('http://localhost:8080/get-nosql-library')
      this.noSqlBooks = response.data
    },
    async createNoSqlBook() {
      await axios.post('http://localhost:8080/create-nosql-book', this.newNoSqlBook)

      await this.getBooksNoSql()

      this.newNoSqlBook.title = ''
      this.newNoSqlBook.genre = ''
    },
    async deleteNoSqlBook(bookId) {
      await axios.delete('http://localhost:8080/delete-nosql-book/' + bookId)

      await this.getBooksNoSql()
    },
  },
  created() {
    this.getBooksSql()
    this.getBooksNoSql()
  }
}
</script>
