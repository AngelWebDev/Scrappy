<template v-slot:extension>
  <v-container fluid class="arrival_container">
    <h1 class="tab-title text-left pb-16">{{ $t("side-bar.arrival") }}</h1>
    <v-row>
      <v-col cols="5">
        <v-autocomplete
          v-model="form.customer_id"
          :items="customers"
          outlined
          dense
          chips
          small-chips
          :label="$t('table-data.customer')"
          v-on:change="onChange"
        />
        <v-select
          dense
          :items="materials"
          v-model="form.material_id"
          :label="$t('table-data.material')"
          outlined
        />
        <v-text-field
          dense
          :label="$t('table-data.weight')"
          v-model="form.gross_weight_kg"
          outlined
          suffix="kg"
        />
        <v-text-field
          dense
          :label="$t('table-data.tare')"
          v-model="form.tare_kg"
          outlined
          suffix="kg"
        />
      </v-col>
      <v-col cols="7" class="text-left pr-12">
        <v-simple-table v-if="customer.id !== null">
          <template v-slot:default>
            <tbody>
              <tr>
                <td>{{ $t("table-data.name") }}:</td>
                <td>{{ customer.firstname + " " + customer.lastname }}</td>
              </tr>
              <tr>
                <td>{{ $t("table-data.company") }}:</td>
                <td>{{ customer.company.name }}</td>
              </tr>
              <tr>
                <td>{{ $t("table-data.address") }}:</td>
                <td>{{ customer.street }}</td>
              </tr>
              <tr>
                <td>
                  {{ $t("table-data.zip") }} / {{ $t("table-data.city") }}:
                </td>
                <td>{{ customer.zip + "/" + customer.city }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-btn depressed @click="cancel">
          {{ $t("form-data.clear") }}
        </v-btn>
      </v-col>
      <v-col cols="6">
        <v-btn depressed color="primary" @click="save">
          {{ $t("form-data.save") }}
        </v-btn>
      </v-col>
    </v-row>
    <br />
    <br />
    <div class="text-center" v-if="error">
      <span class="red--text">{{ error }} </span>
    </div>
  </v-container>
</template>

<script>
import { getCustomers, getCustomer, createArrival } from "../api";
export default {
  name: "arrival",
  data() {
    return {
      customers: [],
      customer: {
        id: null,
        firstname: "",
        lastname: "",
        street: null,
        zip: null,
        city: null,
        company: {
          id: "",
          name: "",
          tax_id: "",
          vat_id: "",
        },
      },
      materials: [
        { value: 1, text: "Cooper" },
        { value: 2, text: "Iron" },
        { value: 3, text: "Wood" },
        { value: 4, text: "Ceramics" },
      ],
      form: {
        customer_id: null,
        material_id: "Cooper",
        gross_weight_kg: 0,
        tare_kg: 0,
      },
      error: "",
      token: "",
    };
  },
  created() {
    this.token = document
      .querySelector('input[name="csrfmiddlewaretoken"]')
      .getAttribute("value");
    this.initialize();
  },
  methods: {
    initialize() {
      getCustomers(this.token)
        .then((res) => res.json())
        .then(({ result }) => {
          console.log("result", result);
          this.customers = result.map((item) => ({
            value: item.id,
            text: item.company
              ? item.firstname +
                " " +
                item.lastname +
                ", " +
                item.company.name +
                ", " +
                item.street +
                ", " +
                item.zip
              : item.firstname +
                " " +
                item.lastname +
                ", " +
                item.street +
                ", " +
                item.zip,
          }));
        });
    },
    onChange(id) {
      getCustomer(id, this.token).then((res) => {
        if (res) {
          if (!res.result.company) {
            res.result.company = Object.assign(
              {},
              {
                id: "",
                name: "",
                tax_id: "",
                vat_id: "",
              }
            );
          }
          this.customer = Object.assign({}, res.result);
        }
      });
    },
    save() {
      createArrival(this.form, this.token).then((res) => {
        if (res.status === 200) {
          this.cancel();
        } else {
          this.error = "Something went wrong";
        }
      });
    },
    cancel() {
      this.customer = Object.assign(
        {},
        {
          id: null,
          firstname: "",
          lastname: "",
          street: null,
          zip: null,
          city: null,
          company: {
            id: "",
            name: "",
            tax_id: "",
            vat_id: "",
          },
        }
      );
      this.form = Object.assign(
        {},
        {
          customer_id: null,
          material_id: null,
          gross_weight_kg: 0,
          tare_kg: 0,
        }
      );
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.arrival_container {
  width: calc(100% - 260px);
  margin-top: 140px;
  margin-left: 260px;
  padding: 30px;
}
</style>
