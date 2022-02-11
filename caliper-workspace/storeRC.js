/*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

'use strict';

const RateInterface = require('/home/ubuntu/caliper-workspace/node_modules/@hyperledger/caliper-core/lib/worker/rate-control/rateInterface.js');
let Sleep = require('/home/ubuntu/caliper-workspace/node_modules/@hyperledger/caliper-core/lib/common/utils/caliper-utils').sleep;

/**
 * Rate controller for allowing uninterrupted workloadload generation.
 *
 * @property {object} options The user-supplied options for the controller. Empty.
 */
class StoreRC extends RateInterface{

    /**
     * Initializes the rate controller instance.
     * @param {TestMessage} testMessage start test message
     * @param {TransactionStatisticsCollector} stats The TX stats collector instance.
     * @param {number} workerIndex The 0-based index of the worker node.
     */
     constructor(testMessage, stats, workerIndex) {
        super(testMessage, stats, workerIndex);

        const tps = this.options.tps ? this.options.tps : 10;
        const tpsPerWorker = tps / this.numberOfWorkers;
        this.sleepTime = (tpsPerWorker > 0) ? 1000/tpsPerWorker : 0;
    }

    /**
     * Perform the rate control action by blocking the execution for a certain amount of time.
     * @async
     */
    async applyRateControl() {
        if (this.sleepTime === 0) {
            return;
        }

        const totalSubmitted = this.stats.getTotalSubmittedTx();
        const diff = (this.sleepTime * totalSubmitted - (Date.now() - this.stats.getRoundStartTime()));
        const prove_time = 146;
        await Sleep(diff + prove_time);
    }

    /**
     * Notify the rate controller about the end of the round.
     * @async
     */
    async end() { }
}

/**
 * Creates a new rate controller instance.
 * @param {object} opts The rate controller options.
 * @param {number} clientIdx The 0-based index of the client who instantiates the controller.
 * @param {number} roundIdx The 1-based index of the round the controller is instantiated in.
 * @return {RateInterface} The rate controller instance.
 */
 function createRateController(testMessage, stats, workerIndex) {
    return new StoreRC(testMessage, stats, workerIndex);
}

module.exports.createRateController = createRateController;