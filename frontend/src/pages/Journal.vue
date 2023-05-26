<template>
  <Header></Header>
  <div class="container" :key="updated">
<!--      {{ journal }}-->
      <section class="journal__head">
          <h1>{{ journal.groupName }}</h1>
          <div v-if="can_edit" class="control">
            <section v-if="placeholder === null"
                     class="bnts__change">
                <button @click="changePlaceholder(0)" class="btn__clear">Убрать</button>
                <button @click="changePlaceholder(1)" class="btn__state1">ОТ</button>
                <button @click="changePlaceholder(2)" class="btn__state2">УП</button>
            </section>
            <section v-else class="btns__save__rollback">
                <button @click="saveChanges" class="btn__save btn__clear">Сохранить</button>
                <button @click="rollbackChanges" class="btn__rollback btn__state2">Отменить</button>
            </section>
          </div>
      </section>
      <section class="journal__table">
          <section class="students__list">
              <div v-for="student in journal.students" class="student">
                  {{student.fullName}}
              </div>
          </section>
          <section class="period">
              <div v-for="date in period" class="date">
                  <span class="date__info">{{date[8] + date[9]}}</span>
                  <div
                          @click="addChanges($event, student, date)"
                          v-for="student in journal.students"
                          class="table__student">
                      <div v-if="this.getState(date, student) === -1" class="state"></div>
                      <div v-if="this.getState(date, student) === 0" id="state0" class="state"></div>
                      <div v-if="this.getState(date, student) === 1" id="state1" class="state"></div>
                      <div v-if="this.getState(date, student) === 2" id="state2" class="state"></div>
                  </div>
              </div>
          </section>
      </section>
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
import axios from "axios";

export default {
    name: "Journal",
    components: {Header},
    data() {
        return {
            journal_id: parseInt(this.$route.params.journal_id, 10),
            journal: {},
            table: {},
            period: this.getCurrentPeriod(),
            changes: [],
            clear: false,
            state1: false,
            state2: false,
            placeholder: null,
            user_id: parseInt(localStorage.getItem('user_id')),
            can_edit: false,
            updated: 0
        }
    },
    methods: {
        canEdit(){
            return this.user_id === this.journal.owner.id;
        },
        async getJournalHead() {
            const resp = await axios.get(`/api/journal/${this.journal_id}`)
            this.journal = resp.data
            this.can_edit = resp.data.owner.id === this.user_id
        },
        async getJournalTable() {
            const resp = await axios.get(`/api/journal/${this.journal_id}/table`,
                {params: {
                        date_start: this.period[0],
                        date_end: this.period[this.period.length-1]
                    }}
            )
            this.table = resp.data
        },

        getCurrentPeriod() {
            const now = Date.now()
            const nowDate = new Date(now)
            const daysInMonth = 33 - new Date(nowDate.getFullYear(), nowDate.getMonth(), 33).getDate();
            console.log(daysInMonth)
            let res = []
            for (let i = 1; i <= daysInMonth; i++) {
                let tmp = new Date(nowDate.getFullYear(), nowDate.getMonth(), i+1)
                res.push(tmp.toISOString().split('T')[0])
            }
            return res
        },
        alreadyInChanges(change) {
            for (let i = 0; i < this.changes.length; i++) {
                if (this.changes[i].student_id === change.student_id
                && this.changes[i].journal_id === change.journal_id
                && this.changes[i].state === change.state
                && this.changes[i].date === change.date) {
                    return true;
                }
            }
            return false;
        },
        addChanges(e, student, date) {
            if (this.placeholder === null) {
                return;
            }

            let changeElem = {
                'student_id': student.id,
                'journal_id': this.journal_id,
                'state': this.placeholder,
                'date': date
            }

            if (this.alreadyInChanges(changeElem)) {
                this.changes = this.changes.filter(object => {
                    return (object.journal_id !== changeElem.journal_id
                        && object.student_id !== changeElem.student_id
                        && object.state !== changeElem.state
                        && object.date !== changeElem.date)
                })
                e.target.id = ''
                return;
            }
            this.changes.push(changeElem)
            e.target.id = 'state'+this.placeholder
        },
        getState(date, student) {
            for (let i = 0; i < this.table.length; i++) {
                if (this.table[i].date === date
                    && this.table[i].student_id === student.id) {
                    return this.table[i].state
                }
            }
            return -1;
        },
        changePlaceholder(state) {
            this.placeholder = state
        },
        async saveChanges() {
            const resp = await axios.post(`/api/journal/${this.journal_id}/table`, this.changes)
            this.changes = []
            this.placeholder = null
            await this.getJournalTable()
        },
        async rollbackChanges() {
            this.placeholder = null
            this.changes = []
            await this.getJournalTable()
            this.updated++
        }
    },
    mounted() {
        this.getJournalHead()
        this.getJournalTable()
    }
}
</script>

<style scoped>
/*#state0 {*/
/*    background-color: #6ad002;*/
/*}*/
#state1 {
    background-color: orange;
}
#state2 {
    background-color: orangered;
}

.state, .state0, .state1, .state2 {
    width: 100%;
    height: 100%;
}
.state0 {
    background-color: #6ad002;
}
.state1 {
    background-color: orange;
}
.state2 {
     background-color: orangered;
}
.container {
    box-shadow: var(--box-shadow-default);
    border-radius: 1rem;
    width: 1640px;
    margin: 50px auto;
}
.journal__head {
    /*margin-top: 50px;*/
    padding-top: 1rem;
    margin-left: 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.bnts__change, .btns__save__rollback {
    padding-right: 25px;
}

.bnts__change button, .btns__save__rollback button {
    min-width: 100px;
    margin-right: 10px;
}
.bnts__change button, .btns__save__rollback button {
    border: none;
    border-radius: 0.25rem;
    box-shadow: var(--box-shadow-default);
}

.btn__clear {
    background-color: lawngreen;
    transition: 175ms;
}
.btn__clear:hover {
    background-color: #6ad002;
}
.btn__clear:active {
    background-color: #5fc001;
}

.btn__state1 {
    background-color: orange;
    transition: 175ms;
}
.btn__state1:hover {
    background-color: #d98f01;
}
.btn__state1:active {
    background-color: #c78102;
}

.btn__state2 {
    background-color: orangered;
    transition: 175ms;
}
.btn__state2:hover {
    background-color: #d53a01;
}
.btn__state2:active {
    background-color: #b03102;
}

.journal__table {
    margin-top: 10px;
    padding: 20px;
    display: flex;
    flex-direction: row;
}

.students__list {
    width: 200px;
    border-right: 1px #eaeaea solid;
    margin-top: 1.75em;
}

.student {
    border-bottom: 1px #eaeaea solid;
    height: 1.75rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.period {
    display: flex;
    flex-direction: row;
}

.date {
    width: 1.75rem;
    text-align: center;
    border-right: 1px #eaeaea solid;
    display: flex;
    flex-direction: column;
}

.date__info {
    height: 1.75em;
    border-bottom: 1px #eaeaea solid;
}

.table__student {
    width: 1.75em;
    height: 1.75em;
    text-align: center;
    border-bottom: 1px #eaeaea solid;
}
</style>