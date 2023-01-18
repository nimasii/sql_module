import { getSecondaryRangeChannel } from '../../channel';
import { channelDefType, getFieldOrDatumDef, isFieldDef, isPositionFieldOrDatumDef } from '../../channeldef';
import { formatCustomType, isCustomFormatType } from '../format';
export function labels(model, channel, specifiedLabelsSpec) {
    var _a;
    const { encoding, config } = model;
    const fieldOrDatumDef = (_a = getFieldOrDatumDef(encoding[channel])) !== null && _a !== void 0 ? _a : getFieldOrDatumDef(encoding[getSecondaryRangeChannel(channel)]);
    const axis = model.axis(channel) || {};
    const { format, formatType } = axis;
    if (isCustomFormatType(formatType)) {
        return Object.assign({ text: formatCustomType({
                fieldOrDatumDef,
                field: 'datum.value',
                format,
                formatType,
                config
            }) }, specifiedLabelsSpec);
    }
    else if (format === undefined && formatType === undefined && config.customFormatTypes) {
        if (channelDefType(fieldOrDatumDef) === 'quantitative') {
            if (isPositionFieldOrDatumDef(fieldOrDatumDef) &&
                fieldOrDatumDef.stack === 'normalize' &&
                config.normalizedNumberFormatType) {
                return Object.assign({ text: formatCustomType({
                        fieldOrDatumDef,
                        field: 'datum.value',
                        format: config.normalizedNumberFormat,
                        formatType: config.normalizedNumberFormatType,
                        config
                    }) }, specifiedLabelsSpec);
            }
            else if (config.numberFormatType) {
                return Object.assign({ text: formatCustomType({
                        fieldOrDatumDef,
                        field: 'datum.value',
                        format: config.numberFormat,
                        formatType: config.numberFormatType,
                        config
                    }) }, specifiedLabelsSpec);
            }
        }
        if (channelDefType(fieldOrDatumDef) === 'temporal' &&
            config.timeFormatType &&
            isFieldDef(fieldOrDatumDef) &&
            !fieldOrDatumDef.timeUnit) {
            return Object.assign({ text: formatCustomType({
                    fieldOrDatumDef,
                    field: 'datum.value',
                    format: config.timeFormat,
                    formatType: config.timeFormatType,
                    config
                }) }, specifiedLabelsSpec);
        }
    }
    return specifiedLabelsSpec;
}
//# sourceMappingURL=encode.js.map