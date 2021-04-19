<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :search="search"
    class="elevation-1"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-text-field
          v-model="search"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
        <v-spacer></v-spacer>

        <v-dialog v-model="dialog" max-width="900px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="primary"
              fab
              dark
              class="mb-2"
              v-bind="attrs"
              v-on="on"
            >
              <v-icon dark>mdi-plus</v-icon>
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">{{ $t(`form-data.${formTitle}`) }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="7" sm="7">
                    <v-row>
                      <v-col cols="4">
                        <v-select
                          outlined
                          :items="solutations"
                          :label="$t('table-data.solutation')"
                          v-model="editedItem.title"
                        ></v-select>
                      </v-col>
                      <v-col cols="8">
                        <v-text-field
                          outlined
                          v-model="editedItem.email"
                          label="Email"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col cols="6">
                        <v-text-field
                          outlined
                          v-model="editedItem.firstname"
                          :label="$t('table-data.firstname')"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="6">
                        <v-text-field
                          outlined
                          v-model="editedItem.lastname"
                          :label="$t('table-data.lastname')"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                    <v-text-field
                      outlined
                      v-model="editedItem.street"
                      :label="$t('table-data.address')"
                    ></v-text-field>
                    <v-row>
                      <v-col cols="6">
                        <v-text-field
                          outlined
                          v-model="editedItem.zip"
                          :label="$t('table-data.zip')"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="6">
                        <v-text-field
                          outlined
                          v-model="editedItem.city"
                          :label="$t('table-data.city')"
                        ></v-text-field>
                      </v-col>
                    </v-row>

                    <v-text-field
                      outlined
                      v-model="editedItem.phone1"
                      :label="$t('table-data.phone')"
                    ></v-text-field>
                    <v-textarea
                      outlined
                      v-model="editedItem.comments"
                      :label="$t('table-data.comments')"
                    ></v-textarea>
                  </v-col>

                  <v-col cols="5">
                    <v-switch
                      outlined
                      class="mb-11"
                      v-model="is_company"
                      :value="is_company"
                      inset
                      :label="$t('table-data.is_company')"
                    />
                    <v-text-field
                      outlined
                      v-show="is_company"
                      v-model="editedItem.company.name"
                      :label="$t('table-data.company_name')"
                    />
                    <v-text-field
                      outlined
                      v-show="is_company"
                      v-model="editedItem.company.vat_id"
                      :label="$t('table-data.vat_id')"
                    />
                    <v-text-field
                      outlined
                      v-show="is_company"
                      v-model="editedItem.company.tax_id"
                      :label="$t('table-data.tax_id')"
                    />
                    <div
                      class="text-right mt-16 pt-16"
                      v-if="!editedItem.identification.length"
                    >
                      <v-btn color="warning" dark @click="openDialogID">
                        {{ $t("table-data.verify") }}
                      </v-btn>
                    </div>

                    <div
                      class="text-left"
                      v-if="editedItem.identification.length"
                    >
                      <h2 class="text-left py-8">
                        {{ $t("table-data.id") }}
                      </h2>
                      <v-row>
                        <v-data-table
                          :headers="idHeaders"
                          :items="editedItem.identification"
                          :hide-default-footer="true"
                          class="elevation-2"
                        >
                          <template v-slot:[`item.actions`]="{ item }">
                            <v-icon small @click="deleteIDItem(item)">
                              mdi-delete
                            </v-icon>
                          </template></v-data-table
                        >
                      </v-row>
                      <div class="text-left pt-4">
                        <v-btn @click="openDialogID">
                          {{ $t("table-data.new") }}
                        </v-btn>
                      </div>
                    </div>
                  </v-col>
                </v-row>
                <div class="text-center" v-if="error">
                  <span class="red--text">{{ error }} </span>
                </div>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-container>
                <v-row>
                  <v-col cols="9">
                    <v-btn color="grey darken-1" text @click="close">
                      {{ $t("form-data.cancel") }}
                    </v-btn>
                    <v-btn color="red darken-1" text @click="deactive">
                      {{ $t("form-data.deactive") }}
                    </v-btn>
                  </v-col>

                  <v-col cols="3">
                    <v-btn color="blue darken-1" text @click="save">
                      {{ $t("form-data.save") }}
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <v-dialog v-model="dialogID" max-width="600px">
          <v-card height="750px">
            <v-card-title>
              <span class="headline">{{ $t(`form-data.id_person`) }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="12">
                    <p class="text-left pa-0 ma-0">
                      {{ editedItem.firstname + " " + editedItem.lastname }}
                    </p>
                    <p class="text-left pa-0 ma-0">
                      {{ editedItem.street }}
                    </p>
                    <p class="text-left ma-0">
                      {{ editedItem.zip + " " + editedItem.city }}
                    </p>
                    <p class="text-left mt-0 mb-8">
                      {{ editedItem.company.name }}
                    </p>
                    <v-row>
                      <v-col cols="12" class="py-0">
                        <v-select
                          outlined
                          :items="types"
                          :label="$t('table-data.doc_type')"
                          v-model="editedItem.identification.document_type"
                        ></v-select>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col cols="12" class="py-0">
                        <v-text-field
                          outlined
                          v-model="editedItem.identification.document_id_number"
                          :label="$t('table-data.doc_number')"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col cols="12" class="py-0">
                        <v-text-field
                          outlined
                          v-model="editedItem.identification.issuing_country"
                          :label="$t('table-data.doc_issuer')"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col cols="12" class="py-0">
                        <v-text-field
                          outlined
                          v-model="editedItem.identification.name_on_document"
                          :label="$t('table-data.doc_name')"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col cols="12" class="py-0">
                        <v-menu
                          v-model="fromDateMenu"
                          :close-on-content-click="false"
                          :nudge-right="40"
                          lazy
                          transition="scale-transition"
                          offset-y
                          full-width
                          max-width="290px"
                          min-width="290px"
                        >
                          <template v-slot:activator="{ on }">
                            <v-text-field
                              outlined
                              :label="$t('table-data.doc_exp')"
                              readonly
                              :value="
                                editedItem.identification
                                  .document_expiration_date
                              "
                              v-on="on"
                            ></v-text-field>
                          </template>
                          <v-date-picker
                            locale="en-in"
                            v-model="
                              editedItem.identification.document_expiration_date
                            "
                            no-title
                            @input="fromDateMenu = false"
                          ></v-date-picker>
                        </v-menu>
                      </v-col>
                    </v-row>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-container>
                <v-row>
                  <v-col cols="6">
                    <v-btn color="grey darken-1" text @click="cancelDoc">
                      {{ $t("form-data.cancel") }}
                    </v-btn>
                  </v-col>

                  <v-col cols="6">
                    <v-btn color="blue darken-1" text @click="saveDoc">
                      {{ $t("form-data.save") }}
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="headline"
              >Are you sure you want to delete this Customer?</v-card-title
            >
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDelete"
                >Cancel</v-btn
              >
              <v-btn color="blue darken-1" text @click="deleteItemConfirm"
                >OK</v-btn
              >
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>

    <template v-slot:[`header.firstname`]="{ header }">
      {{ $t(`table-data.${header.value}`) }}
    </template>
    <template v-slot:[`header.lastname`]="{ header }">
      {{ $t(`table-data.${header.value}`) }}
    </template>
    <template v-slot:[`header.address`]="{ header }">
      {{ $t(`table-data.${header.value}`) }}
    </template>
    <template v-slot:[`header.city`]="{ header }">
      {{ $t(`table-data.${header.value}`) }}
    </template>
    <template v-slot:[`header.comments`]="{ header }">
      {{ $t(`table-data.${header.value}`) }}
    </template>
    <template v-slot:[`header.vat_id`]="{ header }">
      {{ $t(`table-data.${header.value}`) }}
    </template>
    <template v-slot:[`header.status`]="{ header }">
      {{ $t(`table-data.${header.value}`) }}
    </template>
    <template v-slot:[`header.actions`]="{ header }">
      {{ $t(`table-data.${header.value}`) }}
    </template>

    <template v-slot:[`item.status`]="{ item }">
      {{ $t(`table-data.${item.status ? "active" : "inactive"}`) }}
    </template>

    <template v-slot:[`item.actions`]="{ item }">
      <v-icon small class="mr-2" @click="editItem(item)">
        mdi-pencil
      </v-icon>
      <v-icon small @click="deleteItem(item)">
        mdi-delete
      </v-icon>
    </template>

    <template v-slot:no-data>
      <v-btn color="primary" @click="initialize">
        Reset
      </v-btn>
    </template>
  </v-data-table>
</template>

<script>
import moment from "moment";
import {
  createCustomer,
  getCustomer,
  updateCustomer,
  deactiveCustomer,
  deleteCustomer,
  getCustomers,
  verifyIdentification,
  deleteIdentification,
} from "../../api";
export default {
  name: "customers",
  data: () => ({
    dialog: false,
    dialogID: false,
    dialogDelete: false,
    pending: false,
    editing: false,
    search: "",
    token: "",
    error: "",
    // eslint-disable-next-line no-undef
    user: authUser,
    is_company: false,
    solutations: ["Mr", "Mrs", "Dr", "Prof"],
    types: [
      { value: "passport", text: "Passport" },
      { value: "idcard", text: "ID Card" },
      { value: "driverlicense", text: "Driver License" },
    ],
    fromDateMenu: false,

    headers: [
      { text: "No", value: "no" },
      { text: "Last Name", value: "lastname" },
      { text: "First Name", value: "firstname" },
      { text: "Address", value: "street" },
      { text: "City", value: "city" },
      { text: "Comments", value: "comments" },
      { text: "Vat_id", value: "company.vat_id" },
      { text: "Status", value: "status" },
      { text: "Actions", value: "actions", sortable: false },
    ],

    idHeaders: [
      { text: "Type", value: "document_type" },
      { text: "Number", value: "document_id_number" },
      { text: "Valid Until", value: "document_expiration_date" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    items: [],
    editedIndex: -1,
    editedItem: {
      title: "",
      firstname: "",
      lastname: "",
      street: "",
      city: "",
      comments: "",
      status: true,
      phone1: "",
      zip: "",
      email: "",
      company: {
        id: "",
        name: "",
        tax_id: "",
        vat_id: "",
      },
      identification: [],
    },
    defaultItem: {
      title: "",
      firstname: "",
      lastname: "",
      street: "",
      city: "",
      phone1: "",
      comments: "",
      status: true,
      zip: "",
      email: "",
      company: {
        id: "",
        name: "",
        tax_id: "",
        vat_id: "",
      },
      identification: {
        document_type: "passport",
        document_id_number: "",
        name_on_document: null,
        issuing_country: null,
        document_expiration_date: null,
      },
    },
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "create-customer" : "edit-customer";
    },
  },

  mounted() {
    this.token = document
      .querySelector('input[name="csrfmiddlewaretoken"]')
      .getAttribute("value");
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      getCustomers(this.token)
        .then((res) => res.json())
        .then(({ result }) => {
          this.items = result.map((item, index) => ({
            ...item,
            no: index + 1,
          }));
        });
    },

    openDialogID() {
      this.dialogID = true;
    },

    cancelDoc() {
      this.dialogID = false;
      // this.editedItem.identification = Object.assign(
      //   {},
      //   this.defaultItem.identification
      // );
    },

    saveDoc() {
      this.editedItem.identification.verified_at = moment(new Date()).format(
        "MM-DD-YYYY hh:mm"
      );
      Object.assign(this.items[this.editedIndex], this.editedItem);
      const data = {
        customer_id: this.editedItem.id,
        document_type: this.editedItem.identification.document_type,
        document_id_number: this.editedItem.identification.document_id_number,
        name_on_document: this.editedItem.identification.name_on_document,
        issuing_country: this.editedItem.identification.issuing_country,
        document_expiration_date: this.editedItem.identification
          .document_expiration_date,
      };
      verifyIdentification(data, this.token);
      this.editedItem.identification.push(data);
      this.dialogID = false;
    },

    editItem(item) {
      getCustomer(item.id, this.token).then((res) => {
        if (res) {
          this.editedIndex = this.items.indexOf(item);
          if (!res.result.company) {
            res.result.company = Object.assign({}, this.defaultItem.company);
          }
          if (!res.result.identification) {
            res.result.identification = Object.assign(
              {},
              this.defaultItem.identification
            );
          }

          if (
            res.result.identification &&
            res.result.identification.verified_at
          ) {
            res.result.identification.verified_at = moment(
              res.result.identification.verified_at
            ).format("MM-DD-YYYY hh:mm");
          }
          this.editedItem = Object.assign({}, res.result);
          if (res.result.company && res.result.company.id) {
            this.is_company = true;
          }
          this.dialog = true;
          this.editing = true;
        }
      });
    },

    deleteItem(item) {
      item.company = Object.assign({}, this.defaultItem.company);
      item.identification = Object.assign({}, this.defaultItem.identification);
      this.editedIndex = this.items.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteIDItem(item) {
      deleteIdentification(item.id, this.token).then(() => {
        this.editedItem.identification.splice(
          this.editedItem.identification.indexOf(item),
          1
        );
      });
    },

    deleteItemConfirm() {
      this.items.splice(this.editedIndex, 1);
      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.editing = false;
      this.pending = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      deleteCustomer(this.editedItem.id, this.token);
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      const that = this;
      if (this.editedItem.company.id === "") {
        delete this.editedItem.company.id;
      }
      if (!this.is_company) {
        delete this.editedItem.company;
      }
      delete this.editedItem.identification;
      if (this.editedIndex > -1) {
        Object.assign(this.items[this.editedIndex], this.editedItem);

        updateCustomer(this.editedItem, this.token).then((res) => {
          if (res.ok) {
            this.editing = true;
            that.close();
          } else {
            this.error = res.statusText;
          }
        });
      } else {
        if (this.editedItem.email) {
          createCustomer(this.editedItem, this.token)
            .then((res) => res.json())
            .then((res) => {
              if (res.result) {
                res.result.company = Object.assign({}, {});
                this.items.push({
                  ...res.result,
                  no: this.items.length + 1,
                });
                that.close();
              } else {
                this.error = "Something went wrong.";
              }
            });
        }
      }
    },

    deactive() {
      deactiveCustomer(this.editedItem.id, this.token);
      this.editedItem.status = false;
      delete this.editedItem.name;
      updateCustomer(this.editedItem, this.token).then(() => {
        Object.assign(this.items[this.editedIndex], this.editedItem);
        this.close();
      });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.elevation-1 {
  margin-left: 260px;
}
</style>
